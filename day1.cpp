#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

int main()
{
    std::ifstream inputFile("/Users/ago/projects/aoc-2024/data/input.txt");

    if (!inputFile.is_open())
    {
        std::cerr << "Error opening file." << std::endl;
        return 1; // Exit with a non-zero status code to indicate an error
    }

    std::string line;

    std::vector<int> row1;
    std::vector<int> row2;

    while (std::getline(inputFile, line))
    {
        std::istringstream iss(line);
        int num1;
        int num2;

        if (iss >> num1)
        {
            // Read the second number
            iss >> num2;

            row1.push_back(num1); // Add num1 to the end of list1
            row2.push_back(num2);
        }
    }

    inputFile.close(); // Close the file when done reading

    std::sort(row1.begin(), row1.end());
    std::sort(row2.begin(), row2.end());

    int differences;

    for (size_t i = 0; i < row1.size(); ++i)
    {
        int result = std::abs(row1[i] - row2[i]);
        differences += result;
    }

    std::cout << "The sum is " << differences << std::endl;

    return 0;
}