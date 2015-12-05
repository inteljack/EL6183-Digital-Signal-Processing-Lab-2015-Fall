function X = stft(x, R, Nfft)
% X = stft(x, R, Nfft)
% Short-time Fourier Transform with 50 percent overlap
%
% Input:
%   x - 1D signal
%   R - block length (must be even)
%   Nfft - length of FFT (Nfft >= R)
%
% % Example:
% load mtlb;  % load mtlb, Fs
% x = mtlb';  % convert to row vector
% R = 512;
% Nfft = 1024;
% X = stft(x, R, Nfft);
% y = inv_stft(X, R, N);
% max(abs(x - y))  % verify perfect reconstruction

% Ivan Selesnick
% Polytechnic Institute of New York University
% revised August 2009

x = x(:).';  % Ensure that x is a row vector.

% cosine window
n = (1:R) - 0.5;
window  = cos(pi*n/R-pi/2);

% to deal with first and last block:
x = [zeros(1,R) x zeros(1,R)];

Nx = length(x);
Nc = ceil(2*Nx/R)-1;        % Number of blocks (cols of X)
L = R/2 * (Nc + 1);
if Nx < L
    x = [x zeros(1,L-Nx)];  % zero pad x as necessary 
end
X = zeros(R,Nc);
i = 0;
for k = 1:Nc
    X(:,k) = window .* x(i + (1:R));   % multiply signal by window
    i = i + R/2;
end
X = fft(X,Nfft);            % FFT applied to each column of X

