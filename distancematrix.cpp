#include "distancematrix.h"
#include <math.h>
#include <iostream>
#include <fstream>
#include <sstream>

distanceMatrix::distanceMatrix(int size)
{
    double *content[size][size];
    size = size;
}

void distanceMatrix::loadFile(std::string file, int type)
{
    std::vector<std::vector<double>> coords = loadCSV(file, 2,3,size);
    switch(type){
        case 0:
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if(j>=i)break;
                float dist = haversine(coords[i], coords[j]);
                content[i][j] = dist;
                content[j][i] = dist;
            }
        }
    }
}

double distanceMatrix::get(int i, int j)
{
    return content[i][j];
}

void distanceMatrix::set(int i, int j, double val)
{
    content[i][j] = val;
}

std::vector<double> distanceMatrix::row(int i)
{
    return content[i];
}

std::vector<std::vector<double>> distanceMatrix::getAll()
{
    return content;
}

double distanceMatrix::haversine(std::vector<double> i, std::vector<double> j)
{
    const float R = 6371e3;
    float phiI = i[0] * M_PI / 180;
    float phiJ = j[0] * M_PI / 180;
    float deltaPhi = (j[0]-i[0]) * M_PI / 180;
    float deltaLambda = (j[1]-i[1]) * M_PI / 180;

    float a = (sin(deltaPhi/2) * sin(deltaPhi/2)) + (cos(phiI) * cos(phiJ) * sin(deltaLambda/2) * sin(deltaLambda/2));
    float c = 2 * atan2(sqrt(a), sqrt(1-a));
    float distance = R * c;
    return distance;
}

std::vector<std::vector<double>> distanceMatrix::loadCSV(std::string file, int col1, int col2, int nodes)
{
    std::string line;

    std::ifstream fin(file);

    std::vector<std::vector<double>> coords;

    int nodesSoFar = 0;

    while (getline (fin, line) && nodesSoFar < nodes) {
        std::vector<double> coord;

        std::istringstream ss(line);
        std::string token;

        int count = 0;

        while(std::getline(ss, token, ',')) {
            if(count == col1 or count == col2){
                coord.push_back(std::stod(token));
            }
            if(count > col2)break;
        }

        coords.push_back(coord);
        nodesSoFar++;
    }

    fin.close();

    return coords;
}
