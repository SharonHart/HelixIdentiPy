import numpy as np
import scipy
import matcompat

# if available import pylab (from matlibplot)
try:
    import matplotlib.pylab as plt
except ImportError:
    pass


def template_matching(T, I):
    # Local Variables: Idata, I, I_NCC, I_SSD, T, IdataIn
    # Function calls: template_matching_gray, template_matching, double, nargin, template_matching_color, size
    # % TEMPLATE_MATCHING is a cpu efficient function which calculates matching
    # % score images between template and an (color) 2D or 3D image.
    # % It calculates:
    # % - The sum of squared difference (SSD Block Matching), robust template
    # %   matching.
    # % - The normalized cross correlation (NCC), independent of illumination,
    # %   only dependent on texture
    # % The user can combine the two images, to get template matching which
    # % works robust with his application.
    # % Both measures are implemented using FFT based correlation.
    # %
    # %   [I_SSD,I_NCC,Idata]=template_matching(T,I,Idata)
    # %
    # % inputs,
    # %   T : Image Template, can be grayscale or color 2D or 3D.
    # %   I : Color image, can be grayscale or color 2D or 3D.
    # %  (optional)
    # %   Idata : Storage of temporary variables from the image I, to allow
    # %           faster search for multiple templates in the same image.
    # %
    # % outputs,
    # %   I_SSD: The sum of squared difference 2D/3D image. The SSD sign is
    # %          reversed and normalized to range [0 1]
    # %   I_NCC: The normalized cross correlation 2D/3D image. The values
    # %          range between 0 and 1
    # %   Idata : Storage of temporary variables from the image I, to allow
    # %           faster search for multiple templates in the same image.
    # %
    # % Example 2D,
    # %   % Find maximum response
    # %    I = im2double(imread('lena.jpg'));
    # %   % Template of Eye Lena
    # %    T=I(124:140,124:140,:);
    # %   % Calculate SSD and NCC between Template and Image
    # %    [I_SSD,I_NCC]=template_matching(T,I);
    # %   % Find maximum correspondence in I_SDD image
    # %    [x,y]=find(I_SSD==max(I_SSD(:)));
    # %   % Show result
    # %    figure,
    # %    subplot(2,2,1), imshow(I); hold on; plot(y,x,'r*'); title('Result')
    # %    subplot(2,2,2), imshow(T); title('The eye template');
    # %    subplot(2,2,3), imshow(I_SSD); title('SSD Matching');
    # %    subplot(2,2,4), imshow(I_NCC); title('Normalized-CC');
    # %
    # % Example 3D,
    # %   % Make some random data
    # %    I=rand(50,60,50);
    # %   % Get a small volume as template
    # %    T=I(20:30,20:30,20:30);
    # %   % Calculate SDD between template and image
    # %    I_SSD=template_matching(T,I);
    # %   % Find maximum correspondence
    # %    [x,y,z]=ind2sub(size(I_SSD),find(I_SSD==max(I_SSD(:))));
    # %    disp(x);
    # %    disp(y);
    # %    disp(z);
    # %
    # % Function is written by D.Kroon University of Twente (February 2011)

    # % Convert images to double
    T = np.double(T)
    I = np.double(I)
    I_NCC = template_matching_gray(T, I)


    return I_NCC


def template_matching_gray(T, I):
    # Local Variables: LocalSumI, Icorr, stdI, Idata, stdT, QSumT, I, I_NCC, I_SSD, LocalQSumI, T_size, outsize, I_size, T, IdataIn, FT, meanIT, FI
    # Function calls: template_matching_gray, real, ifft2, min, max, sum, local_sum, fftn, fft2, nargout, std, length, isempty, sqrt, numel, unpadarray, rot90, rot90_3D, ifftn, size
    # % Calculate correlation output size  = input size + padding template
    T_size = np.shape(T)
    I_size = np.size(I)
    # outsize = I_size + T_size - 1.
    # % calculate correlation in frequency domain

    FT = np.fft.fftn(rot90_3D(T))
    FI = np.fft.fftn(I)
    Icorr = np.real(np.fft.ifftn((FI * FT)))

    # % Calculate Local Quadratic sum of Image and Template
    LocalQSumI = local_sum(np.power(I,2), T)


    LocalSumI = local_sum(I, T)

    # % Standard deviation
    stdI = np.sqrt((LocalQSumI - np.divide(pow(LocalSumI ,2), np.size(T))))

    stdT = np.dot(np.sqrt((np.size(T) - 1.)), np.std(T.flatten(1)))
    # % Mean compensation
    meanIT = np.divide(np.dot(LocalSumI, np.sum(T.flatten(1))), np.size(T))
    I_NCC = 0.5 + (Icorr - meanIT) / np.dot(2. * stdT, max((stdI), np.divide(stdT, 1e5)))
    # % Remove padding
    I_NCC = unpadarray(I_NCC, matcompat.size(I))

    return I_NCC


def rot90_3D(T):
    # Local Variables: T
    # Function calls: rot90_3D, flipdim
    # T = np.fliplr(np.fliplr(np.fliplr(T, 1.), 2.), 3.)
    return np.rot90(T)


def unpadarray(A, Bsize):
    # Local Variables: A, Bsize, B, Bstart, Bend
    # Function calls: unpadarray, ndims, size, ceil
    Bstart = np.ceil(((matcompat.size(A) - Bsize) / 2.)) + 1.
    Bend = Bstart + Bsize - 1.
    if matcompat.ndim(A) == 2.:
        B = A[int(Bstart[0]) - 1:Bend[0], int(Bstart[1]) - 1:Bend[1]]
    elif matcompat.ndim(A) == 3.:
        B = A[int(Bstart[0]) - 1:Bend[0], int(Bstart[1]) - 1:Bend[1], int(Bstart[2]) - 1:Bend[2]]

    return B


def local_sum(I, T):
    T_size = [60,60,60]
    B = I
    s = np.cumsum(B, 0)
    c = s[int(1. + T_size[0]) - 1:0 - 1., :, :] - s[0:0 - T_size[0] - 1., :, :]
    s = np.cumsum(c, 1)
    c = s[:, int(1. + T_size[1]) - 1:0 - 1., :] - s[:, 0:0 - T_size[1] - 1., :]
    s = np.cumsum(c, 2)
    local_sum_I = s[:, :, int(1. + T_size[2]) - 1:0 - 1.] - s[:, :, 0:0 - T_size[2] - 1.]


    return local_sum_I