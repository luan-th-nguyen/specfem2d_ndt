function generate_model

    [x,z] = getxz();
 
    nx = length(x);
    nz = length(z);
    xmin = min(x(:)); 
    xmax = max(x(:));
    zmin = min(z(:));
    zmax = max(z(:));
    
    %%% generate Gaussian random field
    rng(52461)
    [X,Z] = meshgrid(x,z);
    P = 2.*rand(nz, nx) - 1;
    span = 10
    P = gridsmooth(P,span,'gauss');
    P = P/max(abs(P(:)));

    %%% load gll coordinates
    [l,x,z,rho,vp,vs] = loadbycol('DATA/proc000000_rho_vp_vs.dat_output');
    n = length(x);

    %%% interpolate to gll coordinates
    p = griddata(X,Z,P,x,z);
    thresh = 1.e0;
    I = find(vs > thresh);
    
    f = 0.2;
    rho(I) = rho(I) + f*max(abs(rho))*p(I);
    vp(I) = vp(I) + f*max(abs(vp))*p(I);
    vs(I) = vs(I) + f*max(abs(vs))*p(I);
    
    model = [l x z rho vp vs];
    saveascii(model, 'DATA/model_true_rand_ascii')

    
function [x,z] = getxz()
    xmin = 0.;
    xmax = 400; % 0.4 
    zmin = 0.;  
    zmax = 200; % 0.2

    nx = 100;
    nz = 50;
    
    x = linspace(xmin, xmax, nx);
    z = linspace(zmin, zmax, nz);
    
    
function ZS = gridsmooth(Z,span,opt)
%GRIDSMOOTH Smooth grid data.
%   GRIDSMOOTH(Z,SPAN,OPT) smooths grid data by applying filter of length
%   SPAN.

% check input
error(nargchk(2,3,nargin))

if nargin < 3
    opt = 'moving';
end

if span == 0
    ZS = Z;
    return
elseif numel(span) == 1
    span = [span span];
elseif numel(span) == 2
    % pass
else
    error(badval)
end

W = ones(size(Z));

% address NaNs
inan = isnan(Z);
if any(inan)
    Z(inan) = 0;
    W(inan) = 0;
end

switch opt
    case 'moving'
        [nr,nc] = size(Z);
        SL = spdiags(ones(nr,2*span(1)+1),(-span(1):span(1)),nr,nr);
        SR = spdiags(ones(nc,2*span(2)+1),(-span(2):span(2)),nc,nc);
        
        ZS = SL*Z*SR;
        WS = SL*W*SR;
        ZS = ZS./WS;
        
    case {'gauss' 'gaussian'}
        [X,Y] = meshgrid(2*(-span:span),2*(-span:span));
        sigma = diag(span).^2;
        F = gauss2(X,Y,[0 0],sigma);
        F = F/sum(F(:));

        ZS = convn(Z,F,'same');
        WS = convn(W,F,'same');
        ZS = ZS./WS;
        
    case 'laplacian'
        [X,Y] = meshgrid(1:size(Z,2),1:size(Z,1));
        ZS = meshsmooth(X(:),Y(:),Z(:),span,'laplacian');
        ZS = reshape(ZS,size(Z));

    case 'legacy'
        % same as 'moving', except slower
        F = ones(2*span(1)+1,2*span(2)+1)/((2*span(1)+1)*(2*span(2)+1));

        ZS = convn(Z,F,'same');
        WS = convn(W,F,'same');
        ZS = ZS./WS;

end

if any(inan)
    ZS(inan) = NaN;
end


function B = scale(A,lim)
%SCALE scales array.
%   B = SCALE(A,LIM) scales each element of A in such a way that
%   MIN(B(:)) = LIM(1), MAX(B(:)) = LIM(2). 

% check input arguments
error(nargchk(1,2,nargin))

if numel(lim) ~= 2
    error('Argument must be a 2-element vector.')
end

if nargin < 2
    lim = [-1 1];
end

B = lim(1) + (A-min(A(:)))*diff(lim)/diff(minmax(A));



function varargout = loadbycol(file)
%LOADBYCOL Loads text file column by column.

n = nargout;
array = load(file);

for i=1:n
   varargout{i}  = array(:,i);
end


function Z = gauss2(X,Y,mu,sigma)
%GAUSS2 Bivariate Gaussian function.
%   GAUSS2(X,Y,MU,COV) evaluates a Gaussian function with mean MU and
%   covariance SIGMA at the points of X and Y.

assert(isequal(size(X),size(Y)),...
    'SizeError')
assert(isvector(mu),...
    'ValueError')
assert(ismatrix(sigma),...
    'ValueError')

% determinant of covariance matrix
D = sigma(1,1)*sigma(2,2) - sigma(1,2)*sigma(2,1);

% inverse of covariance matrix
B = D^-1 * [sigma(2,2) -sigma(1,2); -sigma(2,1) sigma(1,1)];

% evaluate Gaussian
X = X-mu(1);
Y = Y-mu(2);
Z = B(1,1)*X.^2 + B(1,2)*X.*Y + B(2,1)*X.*Y + B(2,2)*Y.^2;
Z = exp(-0.5*Z);
Z = (2*pi*sqrt(D))^-1 * Z;

