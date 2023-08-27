#ifndef ANT_H
#define ANT_H

#include <vector>

class ant
{
public:
    ant(std::vector<int> nodes, double alpha, double beta);
    void move(std::vector<std::vector<double>> tau, std::vector<std::vector<double>> eta, double alpha, double beta);
    double getCost();
    std::vector<int> getRoute();

private:
    double probabilityIJ(int i, int j, std::vector<std::vector<double>> tau, std::vector<std::vector<double>> eta, double alpha, double beta);
    int nextNode(std::vector<std::vector<double>> tau, std::vector<std::vector<double>> eta, double alpha, double beta);

    int node;
    std::vector<int> remaining;
    double cost;
    std::vector<int> route;
    double alpha;
    double beta;
};

#endif // ANT_H
