#ifndef DISTANCEMATRIX_H
#define DISTANCEMATRIX_H

#include <string>
#include <vector>

class distanceMatrix
{
public:
    distanceMatrix();
    void loadFile(std::string file, int nodes);
    double get(int i, int j);
    void set(int i, int j, double val);
    std::vector<double> row(int i);
    std::vector<std::vector<double>> getAll();
    void print();

private:
    double haversine(std::vector<double> i, std::vector<double> j);
    std::vector<std::vector<double>> loadCSV(std::string file, int col1, int col2, int nodes, bool header);

    std::vector<std::vector<double>> content;
};

#endif // DISTANCEMATRIX_H
