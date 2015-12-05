function y = inv_stft(X, R, N)
% y = inv_stft(X, R, N)
% Inverse Short-time Fourier Transform with 50% overlap
%
% Input:
%   X - STFT produced by 'stft'
%   R - block length
%   N - length of signal

% Ivan Selesnick
% Polytechnic Institute of New York University
% revised August 2009

% get sizes
[Nfft, Nc] = size(X);

% make cosine window
n = (1:R) - 0.5;
window  = cos(pi*n/R-pi/2);

Y = ifft(X);        % inverse FFT of each column of X
Y = Y(1:R,:);       % truncate down to block length
y = zeros(1,R/2*(Nc+1));
i = 0;
for k = 1:Nc
    y(i + (1:R)) = y(i + (1:R)) + window .* Y(:,k).';
    i = i + R/2;
end
% take care of first half-block
y(1:R/2) = y(1:R/2) ./ (window(1:R/2).^2);
% take care of last half-block
y(end-R/2+(1:R/2)) = y(end-R/2+(1:R/2)) ./ (window(R/2+1:R).^2);

y = y(R+(1:N));


