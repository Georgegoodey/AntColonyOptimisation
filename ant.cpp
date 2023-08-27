#include "ant.h"

#include <iostream>
#include <ctime>
#include <cmath>
#include <random>

ant::ant(std::vector<int> nodes, double alpha, double beta)
{
    remaining = nodes;

    srand( time(NULL) );
    int random = rand() % nodes.size();
    node = nodes[random];

    remaining.erase(remaining.begin()+random);

    cost = 0;
    route.push_back(node);
    alpha = alpha;
    beta = beta;
}

void ant::move(std::vector<std::vector<double>> tau, std::vector<std::vector<double>> eta, double alpha, double beta)
{
    int originalNode = node;
    while(!remaining.empty())
    {
        int nodeIndex = nextNode(tau, eta, alpha, beta);
        int newNode = remaining[nodeIndex];
        remaining.erase(remaining.begin()+nodeIndex);
        route.push_back(newNode);
        cost += eta[node][newNode];
        node = newNode;
    }
    route.push_back(originalNode);
    cost += eta[node][originalNode];
    node = originalNode;
}

double ant::getCost()
{
    return cost;
}

std::vector<int> ant::getRoute()
{
    return route;
}

double ant::probabilityIJ(int i, int j, std::vector<std::vector<double>> tau, std::vector<std::vector<double>> eta, double alpha, double beta)
{
    if(eta[i][j] == 0)
    {
        return 0;
    }
    double pheromoneProx = pow(tau[i][j],alpha) * pow(eta[i][j],-beta);
    return pheromoneProx;
}

int ant::nextNode(std::vector<std::vector<double>> tau, std::vector<std::vector<double>> eta, double alpha, double beta)
{
    std::vector<double> probs;

    double sumAllowed =  0;

    for(int n: remaining)
    {
        double prob = probabilityIJ(node,n,tau,eta, alpha, beta);

        sumAllowed += prob;
        probs.push_back(prob);
    }
    for(int i=0; i<probs.size(); i++)
    {
        double prob = probs[i];
        probs[i] = prob / sumAllowed;
    }

    std::random_device rd;
    std::mt19937 gen(rd());
    std::discrete_distribution<> distribution(probs.begin(), probs.end());

    int choice = distribution(gen);

    return choice;
}
