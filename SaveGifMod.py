from PIL import Image
import os
import imageio


def SaveGif(fileNames, outputFile, loopBack):

    with imageio.get_writer(outputFile, mode='I', duration=1/30) as writer:
        count = 0
        for filename in fileNames:
            image = imageio.imread(filename)
            writer.append_data(image)
            print("Saving gif: " + str(100*count / len(fileNames)) + '%')
            count += 1
        if loopBack:
            for i in range(len(fileNames) - 1, 0, -1):
                image = imageio.imread(fileNames[i])
                writer.append_data(image)
        count = 0
        for filename in fileNames:
            print("Removing files: " + str(100*count / len(fileNames)) + "%")
            os.remove(filename)
            count += 1
