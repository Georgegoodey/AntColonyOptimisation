#include "mainwindow.h"
#include "ant.h"
#include "distancematrix.h"

#include <QApplication>
#include <QGraphicsView>
#include <QPushButton>
#include <QLineEdit>
#include <QGraphicsRectItem>
#include <QProgressBar>
#include <QLabel>

#include <iostream>
#include <limits>

int antCount = 10;
int iterations = 10;

QLineEdit *t1;
QLineEdit *t2;
QProgressBar *pb;
QLabel *l1;
QLabel *l2;

static void runACO()
{

    iterations = t1->text().toInt();
    antCount = t2->text().toInt();

    // ACO code
//    std::vector<std::vector<double>> distMat = {
//        {0,  1,  4,  1,  2,  4,  5},
//        {1,  0,  2,  2,  1,  3,  4},
//        {4,  2,  0,  3,  1,  2,  1},
//        {1,  2,  3,  0,  1,  2,  4},
//        {2,  1,  1,  1,  0,  1,  2},
//        {4,  3,  2,  2,  1,  0,  1},
//        {5,  4,  1,  4,  2,  1,  0}
//    };

    int size = 50;

    distanceMatrix distMat = distanceMatrix();
    distMat.loadFile("C:/Users/georg/CSYear3/AntColonyOptimisation/gb.csv",size);

    double alpha = 1;
    double beta = 2;
    double evapCoef = 0.1;
    double q = 1;

    std::vector<std::vector<double>> tau;

    for (int i = 0; i < size; ++i) {
        std::vector<double> tauRow;
        for (int j = 0; j < size; ++j) {
            tauRow.push_back(1);
        }
        tau.push_back(tauRow);
    }

//    std::vector<std::vector<double>> tau = {
//        {1, 1, 1, 1, 1, 1, 1},
//        {1, 1, 1, 1, 1, 1, 1},
//        {1, 1, 1, 1, 1, 1, 1},
//        {1, 1, 1, 1, 1, 1, 1},
//        {1, 1, 1, 1, 1, 1, 1},
//        {1, 1, 1, 1, 1, 1, 1},
//        {1, 1, 1, 1, 1, 1, 1}
//    };

    double bestCost = std::numeric_limits<double>::max();
    std::vector<int> bestRoute;

    for (int i = 0; i < iterations; i++) {
//        std::vector<std::vector<double>> tauChange = {
//            {0, 0, 0, 0, 0, 0, 0},
//            {0, 0, 0, 0, 0, 0, 0},
//            {0, 0, 0, 0, 0, 0, 0},
//            {0, 0, 0, 0, 0, 0, 0},
//            {0, 0, 0, 0, 0, 0, 0},
//            {0, 0, 0, 0, 0, 0, 0},
//            {0, 0, 0, 0, 0, 0, 0}
//        };

        std::vector<std::vector<double>> tauChange;

        for (int i = 0; i < size; ++i) {
            std::vector<double> tauRow;
            for (int j = 0; j < size; ++j) {
                tauRow.push_back(1);
            }
            tauChange.push_back(tauRow);
        }

        for (int a = 0; a < antCount; a++) {
            std::vector<int> nodes;
            for (int i = 0; i < size; i++){
                nodes.push_back(i);
            }
            ant newAnt = ant(nodes,alpha,beta);
            newAnt.move(tau,distMat.getAll(), alpha, beta);
            std::vector<int> route = newAnt.getRoute();
            if(newAnt.getCost() < bestCost)
            {
                bestCost = newAnt.getCost();
                bestRoute = route;
            }
            for (int r=0; r<route.size()-1; r++) {
                tauChange[route[r]][route[r+1]] += q/newAnt.getCost();
            }
            double percent = ((double)i/(double)iterations)+(((double)a/((double)antCount)/(double)iterations));
            pb->setValue(percent*100);
        }
        for (int r=0; r<tau.size(); r++) {
            for (int c=0; c<tau[r].size(); c++) {
                tau[r][c] = tau[r][c] * (1-evapCoef);
                tau[r][c] = tau[r][c] + (tauChange[r][c] / antCount);
            }
        }

    }
    pb->setValue(100);
    QString route;
    for(int i: bestRoute)
    {
        route.append(QString::number(i)+" ");
    }
    l1->setText(route);
    l2->setText(QString::number(bestCost));
}

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;

    std::cout << "Begin \n";

    QPushButton *b = w.findChild<QPushButton*>("pushButton");

    QObject::connect(b,&QPushButton::clicked,runACO);

    t1 = w.findChild<QLineEdit*>("lineEdit");
    t1->setText("10");

    t2 = w.findChild<QLineEdit*>("lineEdit_2");
    t2->setText("10");

    l1 = w.findChild<QLabel*>("label");

    l2 = w.findChild<QLabel*>("label_2");

    pb = w.findChild<QProgressBar*>("progressBar");
    pb->setValue(0);

    w.show();

    return a.exec();
}
