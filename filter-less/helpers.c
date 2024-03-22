#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    double avgcolor;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            avgcolor = (image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.0;
            image[i][j].rgbtRed = image[i][j].rgbtBlue = image[i][j].rgbtGreen = round(avgcolor);
         }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    return;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int red = image[i][j].rgbtRed;

            int sepiaRed = .393*red + .769*green + .189*blue;
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            int sepiaGreen = .349*red + .686*green + .168*blue;
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            int sepiaBlue = .272*red + .534*green + .131*blue;
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
        }
}
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp = image[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[height][width] = image[height][width];
            image[height][width] = image[height][width - j - 1];
            image[height][width] = temp;
        }
    return;
}
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
     RGBTRIPLE newImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            newImage[i][j] = image[i][j];
        }
    }

    for (int i = 0, red, green, blue, counter; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
        red = green = blue = counter = 0;
        if (i + 1 <height && j - 1 >=0)
        {
            red += image[i][j].rgbtRed + image[i + 1][j - 1].rgbtRed;
            green += image[i][j].rgbtGreen + image[i + 1][j - 1].rgbtGreen;
            blue += image[i][j].rgbtBlue + image[i + 1][j - 1].rgbtBlue;
            counter++;
        }
        if (j + 1<width)
        {
            red += image[i][j].rgbtRed + image[i][j + 1].rgbtRed;
            green += image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen;
            blue += image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue;
            counter++;
        }
        if (i + 1 <height && j + 1 <width)
        {
            red += image[i][j].rgbtRed + image[i + 1][j + 1].rgbtRed;
            green += image[i][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen;
            blue += image[i][j].rgbtBlue + image[i + 1][j + 1].rgbtBlue;
            counter++;
        }
        if (i + 1<height)
        {
            red += image[i][j].rgbtRed + image[i + 1][j].rgbtRed;
            green += image[i][j].rgbtGreen + image[i + 1][j].rgbtGreen;
            blue += image[i][j].rgbtBlue + image[i + 1][j].rgbtBlue;
            counter++;
        }
        if (j - 1>=0)
        {
            red += image[i][j].rgbtRed + image[i][j - 1].rgbtRed;
            green += image[i][j].rgbtGreen + image[i][j - 1].rgbtGreen;
            blue += image[i][j].rgbtBlue + image[i][j - 1].rgbtBlue;
            counter++;
        }
        if (i - 1>=0)
        {
            red += image[i][j].rgbtRed + image[i - 1][j].rgbtRed;
            green += image[i][j].rgbtGreen + image[i - 1][j].rgbtGreen;
            blue += image[i][j].rgbtBlue + image[i - 1][j].rgbtBlue;
            counter++;
        }
        newImage[i][j].rgbtRed = red/counter;
        newImage[i][j].rgbtGreen = green/counter;
        newImage[i][j].rgbtBlue = blue/counter;
    }
}
    return;
        }



