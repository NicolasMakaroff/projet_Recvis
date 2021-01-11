import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import matplotlib.image


def add_gaussian_noise(path, sigma) : 
    im = Image.open(path)
    data = np.asarray(im)/255
    
    noise = np.random.normal(0, sigma, size=data.shape)
    res = data + noise
    plt.imshow(res)
    plt.show() 
    res[res<0] = 0
    res[res>1] = 1
    plt.imsave('noisy_'+path, res)
    
    
    
def add_sp_noise(path, p) : 
    im = Image.open(path)
    data = np.asarray(im)/255
    print("nb0 init", np.sum(data==0))
    row,col,ch = data.shape
    if np.all(data[:,:,0]==data[:,:,1]) and np.all(data[:,:,1]==data[:,:,2]):
        noise1 = np.random.choice(data.shape[0],size=int(p*data.size), replace=True)
        noise2 = np.random.choice(data.shape[1],size=int(p*data.size), replace=True)
        bin = np.random.binomial(1,0.5, noise1.size)
        print("taille bin",bin.size)
        for i in range(noise1.size):
            data[noise1[i], noise2[i], 0]= bin[i]
            data[noise1[i], noise2[i], 1]= bin[i]
            data[noise1[i], noise2[i], 2]= bin[i]
    else : 
        noise = np.random.choice(np.arange(data.size),size=int(p*data.size), replace=False)
        bin = np.random.binomial(1,0.5, noise.size)
        print(bin)
        for index, val in enumerate(noise): 
            row_n = val//(col*ch)
            ch_n = val % ch
            col_n = ((val - ch_n) //ch) % col
        #print(data.shape)
        #print(row_n, col_n, ch_n)
            data[row_n, col_n, ch_n] = bin[index]
    plt.imshow(data)
    plt.show() 
    print('taille image', data.size)
    print('taille à changer',data.size*p)
    print('nb 0 apres ', np.sum(data==0))
    plt.imsave('noisy_sp_'+path[:-3]+'png', data)
    
def to_black_white(path): 
    im = Image.open(path)
    #data = np.asarray(im)/255
    data = np.asarray(im) #####
    row,col,ch = data.shape
    if ch==4 : 
        data_bw = np.mean(data[:,:,:-1], axis = 2)
        data_bw3 = np.copy(data)
        for i in range(3):
            data_bw3[:,:,i]= data_bw
    elif ch==3:
        data_bw = np.mean(data, axis = 2)
        data_bw3 = np.repeat(data_bw[:, :, np.newaxis], 3, axis=2)
    else :
        print('Impossible')
        return 
    plt.imshow(data_bw, cmap='gray') #####cmap et databw
    plt.show()
    plt.imsave('bw'+path, data_bw, cmap='gray') 

add_sp_noise('ladefense_orange_loin.jpg', 0.004)
#to_black_white('ladefense2.jpg')
