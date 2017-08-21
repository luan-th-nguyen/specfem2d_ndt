% add path to EOSC454code including sub-folders
close all; clear all;
addpath(genpath('/home/luan/src/others/EOSC454code'))

%% Hanning windowed toneburst
dt = 5.0E-005;
Fs = 1/dt;
N = 2400;
td = dt*N; % time duration of the input signal
delay = 0.0;
fc = 40; % frequency

%% Ricker
Ricker40kHz = load('../data_40kHz/000004/source.txt');
tR40 = Ricker40kHz(:,3);
dR40 = Ricker40kHz(:,2);
Ricker100kHz = load('../data_100kHz/000004/source.txt');
tR100 = Ricker100kHz(:,3);
dR100 = Ricker100kHz(:,2);

dR40 = -dR40/max(abs(dR40));
dR100 = -dR100/max(abs(dR100));
figure(1);
plot(tR40,dR40,'linewidth',1.5); hold on
plot(tR100,dR100,'--r','linewidth',1.5);
set(gca,'fontsize',14)
%xlim([-0.006,0.1]);
xlabel('Time [ms]')
ylabel('Normalized amplitude')
legend('40 kHz (for FWI)','100 kHz (for RTM)');




%% FFT
Nfft = 2400; %2^11;
dR40 = dR40(1:Nfft);
tR40 = tR40(1:Nfft);
dR100 = dR100(1:Nfft);
tR100 = tR100(1:Nfft);
[YR40,fR40] = getFFT(dR40,tR40);
[YR100,fR100] = getFFT(dR100,tR100);
% Plot single-sided amplitude spectrum.
figure(2);
%semilogy(f,abs(Y(1:NFFT/2+1,:))) 
%plot(f,abs(Y(1:NFFT/2+1,:))) 
plot(fR40,abs(YR40),'linewidth',1.5); hold on
plot(fR100,abs(YR100),'--r','linewidth',1.5);
set(gca,'fontsize',12)
%title('Frequency spectra')
xlabel('Frequency [KHz]')
ylabel('|Amplitude|')
legend('40 kHz (for FWI)','100 kHz (for RTM)');
xlim([0 400])

print(1,'-dpng','inputs','-r300');
print(2,'-dpng','inputs_fft','-r300');
