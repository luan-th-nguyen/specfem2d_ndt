close all; clear all;

%% specfem3d simulation
%load('../figs/displ_40kHz_pure.mat');
%load('../figs/displ_40kHz_polluted.mat');
load('../figs/displ_100kHz_pure.mat');
%load('../figs/displ_100kHz_polluted.mat');

data = sim_data;
dt = 5.0e-5; % second
t = [1:size(data,2)]*dt;

%offset = [-120 -80 -40 0 40 80 120 160 200 240]; % shot #000003
offset = [-160 -120 -80 -40 0 40 80 120 160 200]; % shot #000004
shown_ampl = 80.;
max_ampl = max(abs(data(:)));

%% Heidimode simulation
%fid = fopen('/home/luan/src/Heidimod/ultrasonics_ndt/layered_structure_40kHz/000004/arbzseis','r')
fid = fopen('/home/luan/src/Heidimod/ultrasonics_ndt/layered_structure_100kHz/000004/arbzseis','r')

%Matlab erkennt hier nur little endian (falsch)
data1 = fread(fid, inf, 'single', 'ieee-be');
fclose(fid)
% Die Zahlen: 200 200 10 sind die Dimensionen aus dem Header-File !
data1 = reshape(data1,[10 30000]);                          % Heidimod data
dt1 = 5.0e-9*1e3; % second
t1 = [1:size(data1,2)]*dt1;

shown_ampl1 = 80; %20.;
max_ampl1 = max(abs(data1(:)));



figure(1); %  traces before muting
for i=1:size(data,1)
    if i ~= 50
        plot(data(i,1:end)/max_ampl*shown_ampl+offset(i),t(1:end),'k-','linewidth',1.5); hold on
        plot(data1(i,1:end)/max_ampl1*shown_ampl1+offset(i),t1(1:end),'b-','linewidth',1.5); hold on
        %plot(data1(i,1:end)/max_ampl1*shown_ampl1+offset(i),t1(1:end),'b-','linewidth',1.5); hold on
    end
end
set(gca,'fontsize',12)
set(gca,'Ydir','reverse')
fig = gcf;
fig.PaperUnits = 'inches';
fig.PaperPosition = [0 0 6 5];
xlim([offset(1)-20 offset(end)+20]);
%ylim([0. 0.1]);
xlabel('Offset [mm]');
ylabel('Time [ms]');
legend('specfem2d','fd');

%print(1,'-dpng','../figs/model2_disp_40kHz_pure','-r150')
%print(1,'-dpng','../figs/model2_disp_40kHz_polluted','-r150')
%print(1,'-dpng','../figs/model2_disp_100kHz_pure','-r150')
%print(1,'-dpng','../figs/model2_disp_100kHz_polluted','-r150')
print(1,'-dpng','../figs/model2_disp_100kHz_heidimod_specfem2d','-r150')