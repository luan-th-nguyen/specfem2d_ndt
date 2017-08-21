close all
clear all
% Dieses skript liest big endian ein und produziert eine Bilderserie des
% Wellenfeldes
fid_d = fopen('model_init/proc000000_vs.bin','r');
fid_z = fopen('model_init/proc000000_z.bin','r');
fid_x = fopen('model_init/proc000000_x.bin','r');
%[fname, mode, mformat] = fopen(fid) % Diese Zeile ist nicht notwendig,
% Matlab erkennt hier nur little endian (falsch)
data = fread(fid_d, inf, 'single', 'ieee-le');
z = fread(fid_z, inf, 'single', 'ieee-le');
x = fread(fid_x, inf, 'single', 'ieee-le');
data(1) = []; z(1) = []; x(1) = [];
data(end) = []; z(end) = []; x(end) = [];
fclose(fid_d);
fclose(fid_z);
fclose(fid_x);
% Die Zahlen: 200 200 10 sind die Dimensionen aus dem Header-File !
%data = reshape(data,[200 400]);
figure(1)
%pcolor(z,x,data)
dummy = 2000*ones(size(data));
%quiver(x,z,data,dummy);
scatter(x,z,6,mat2gray(data),'filled');
axis equal
%ylim([0 0.2])
%xlim([0 0.4])
%axis tight;
%shading interp;
colorbar;