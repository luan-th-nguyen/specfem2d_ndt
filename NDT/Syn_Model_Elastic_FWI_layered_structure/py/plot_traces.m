%% specfem3d simulation
%load('../figs/displ_40kHz_pure.mat');
%load('../figs/displ_40kHz_polluted.mat');
%load('../figs/displ_100kHz_pure.mat');
load('../figs/displ_100kHz_polluted.mat');

data = sim_data;
dt = 5.0e-5; % second
%offset = [-120 -80 -40 0 40 80 120 160 200 240]; % shot #000003
offset = [-160 -120 -80 -40 0 40 80 120 160 200]; % shot #000004
shown_ampl = 100.;
max_ampl = max(data(:));
t = [1:size(data,2)]*dt;
figure(1); %  traces before muting
for i=1:size(data,1)
    if i ~= 5
        plot(data(i,1:end)/max_ampl*shown_ampl+offset(i),t(1:end),'k-','linewidth',1.5); hold on
        %plot(data(i,1:end)/max_ampl*shown_ampl+offset(i),t(1:end),'k-','linewidth',2); hold on
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

%print(1,'-dpng','../figs/model2_disp_40kHz_pure','-r150')
%print(1,'-dpng','../figs/model2_disp_40kHz_polluted','-r150')
%print(1,'-dpng','../figs/model2_disp_100kHz_pure','-r150')
print(1,'-dpng','../figs/model2_disp_100kHz_polluted','-r150')