#include "distancematrix.h"
#include <math.h>
#include <iostream>
#include <fstream>
#include <sstream>

distanceMatrix::distanceMatrix(){

}

void distanceMatrix::loadFile(std::string file, int nodes)
{
    std::vector<std::vector<double>> coords = loadCSV(file,2,3,nodes,true);
    for (int i = 0; i < coords.size(); i++) {
        std::vector<double> newRow;
        for (int j = 0; j < coords.size(); j++) {
            if(i == j){
                newRow.push_back(0);
                continue;
            }
            double dist = haversine(coords[i], coords[j]);
            newRow.push_back(dist);
        }
        content.push_back(newRow);
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

void distanceMatrix::print()
{
    for (int i = 0; i < content.size(); i++)
    {
        for (int j = 0; j < content[i].size(); j++)
        {
            std::cout << content[i][j] << " ";
        }
        std::cout<< "\n";
    }
}

double distanceMatrix::haversine(std::vector<double> i, std::vector<double> j)
{
    const double R = 6371e3;
    double phiI = i[0] * M_PI / 180;
    double phiJ = j[0] * M_PI / 180;
    double deltaPhi = (j[0]-i[0]) * M_PI / 180;
    double deltaLambda = (j[1]-i[1]) * M_PI / 180;

    double a = (sin(deltaPhi/2) * sin(deltaPhi/2)) + (cos(phiI) * cos(phiJ) * sin(deltaLambda/2) * sin(deltaLambda/2));
    double c = 2 * atan2(sqrt(a), sqrt(1-a));
    double distance = R * c;
    return distance;
}

std::vector<std::vector<double>> distanceMatrix::loadCSV(std::string file, int col1, int col2, int nodes, bool header)
{
    std::string line;

    std::ifstream fin(file);

    std::vector<std::vector<double>> coords;

    int nodesSoFar = 0;

    if(header)getline(fin,line);

    while (getline (fin, line) && nodesSoFar < nodes) {
        std::vector<double> coord;

        std::istringstream ss(line);
        std::string token;

        int count = 0;

        while(std::getline(ss, token, ',')) {
            count++;
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
