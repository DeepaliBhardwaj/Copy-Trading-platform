# Vega - CopyTrading Program

## Overview

Vega is a sophisticated CopyTrading Program designed to empower users in their stock market endeavors. This program is a valuable tool for both beginners and experienced traders, providing a seamless platform for practicing stock market analysis through copy trading. By offering real-time input of stock prices, technical indicators, and trade details, Vega enables users to evaluate their trading strategies, track performance, and make informed decisions in a dynamic market environment.

### Key Features

- **Copy Trading Functionality**: Users can replicate trades by inputting current stock prices and desired sell prices.
  
- **Real-Time Data Analysis**: The program performs detailed analysis of trade data, providing insights into profit margins, win/loss ratios, and overall trading performance.
  
- **Graphical Data Visualization**: Visual representations of trading data, including graphs and charts, allow users to easily interpret and analyze their trading patterns.

- **Multi-Format Data Storage**: Vega ensures data accessibility and security through storage in MongoDB (local and cloud) and JSON files.

- **Self-Destruct Mode**: An added security feature, allowing the program to wipe data under specific conditions, such as a command from the server.

## Installation

### Prerequisites

Before installing Vega, ensure you have the following prerequisites:

- Python 3.10 or higher installed on your system.
- The required Python packages listed in `requirements.txt`.

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/vega-copytrading.git
   ```
   
2. **Navigate to the Project Directory:**
   ```bash
   cd vega-copytrading
   ```

3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Getting Started

To use Vega and explore its functionalities, follow these steps:

1. **Run the Program:**
   ```bash
   python StockAverage.py
   ```
   
2. **Input Trade Details:**
   - Enter the current bidding price of the stock.
   - Input the desired closing price for selling the stock.
   - Specify the number of technical indicators used in the trade.
   - Provide the names of the indicators utilized (if applicable).
   - Enter the name of the stock being traded.

3. **Analyze and Interpret Data:**
   - Review the output data, including total profit/loss, average performance, and win/loss ratios.
   - Explore the graphical visualizations to gain insights into trading patterns, indicator success rates, and historical performance.

4. **Continue or Exit:**
   - Input 'c' to continue trading with additional trades.
   - Input 'e' to exit the program.

### Data Analysis and Visualization

- **Total Profit/Loss Analysis:** Vega calculates the total profit or loss from all trades, providing an overview of the user's financial performance.
  
- **Average Profit/Loss Comparison:** Users can compare the average profit or loss per trade to assess the overall success of their trading strategy.
  
- **Win/Loss Ratio Evaluation:** The program analyzes the number of winning and losing trades to determine the user's success rate.
  
- **Indicator Usage Analysis:** Graphs visualize the success rates of different technical indicators, aiding users in identifying effective trading strategies.
  
- **Historical Trade Performance:** A histograph displays the success of specific trades over time, enabling users to refine their strategies based on past performance.

### Data Storage Options

Vega offers multiple data storage options to suit the user's preferences and requirements:

1. **Local MongoDB:** Data stored locally on the user's machine for easy access and retrieval.
  
2. **MongoDB Cloud Server:** Data stored on a cloud server, providing remote access and backup capabilities.
  
3. **JSON Files:** Data stored in JSON format, ensuring offline access and portability.

### Self-Destruct Mode

As a security measure, Vega includes a self-destruct mode feature. This feature allows the program to wipe its data under specific conditions, such as receiving a command from the server. This ensures that sensitive trading data remains secure and protected.

## License

This project is licensed under the [Apache 2.0 License](LICENSE).

## Contact Information

For questions, suggestions, or feedback regarding Vega - CopyTrading Program, please feel free to reach out:

- **Rahul Vishwakarma**
- Email: karmarahul67@gmail.com

## Acknowledgements

Vega - CopyTrading Program acknowledges the contributions of various tools and technologies that have made this project possible:

- **Python Community**: For the powerful libraries and frameworks used in development.
  
- **MongoDB**: Providing robust data storage solutions for local and cloud-based applications.
  
- **GitHub**: Offering version control and hosting services for collaborative development.

---

This detailed documentation provides users with comprehensive insights into the features, functionalities, and usage of Vega - CopyTrading Program. It serves as a guide for users to navigate the program effectively and make the most out of their stock market trading experience.
