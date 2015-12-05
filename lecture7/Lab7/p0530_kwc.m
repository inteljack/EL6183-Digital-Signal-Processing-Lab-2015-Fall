
[input, Fs] = wavread('10_100.wav');
[b a] = butter(2, [40 70]./(Fs/2), 'stop');
%h = fvtool(b,a);
d = designfilt('bandstopiir','FilterOrder',2, ...
               'HalfPowerFrequency1',59,'HalfPowerFrequency2',61, ...
               'DesignMethod','butter','SampleRate',Fs)
d.Coefficients           
Nfft = 1024
output= filtfilt(d,input);
% ?subplot(2,1,1)
% input_fft = fft(input ,Nfft)
% plot(Nfft,input_fft)
% output_fft = fft(output,Nfft)
% subplot(2,1,2)
% plot(Nfft,output_fft)
soundsc(output);
