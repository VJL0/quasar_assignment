DEMO:

https://i.imgur.com/8OVMUFI.gif

👉🏿<img src='https://i.imgur.com/8OVMUFI.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

1. Clone this repo and create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   #Mac command
   venv\Scripts\activate      #Windows command
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app from the project root:
   ```bash
   python main.py
   ```

- The script will generate an interactive file called `plot.html`.
- It will automatically try to open in your default web browser.
- If it doesn’t open automatically, you can open `plot.html` manually in Chrome.

Notes on design choices:

- I chose Plotly because it already has built-in interactive plots.
- I had assistance from chatGPT, as I am new to both Pandas and Plotly. It generated most of the code, and I modified it to fit my desired UI.
- I decided to have multiple subplots to allow the users to focus on one metric at a time and compare them easily. This also solved the stretching issue when having multiple lines in one plot.
- I added buttons to filter by quartile to allow users to focus on specific data ranges.
- I set the legend to be right side of the plot area to have more Y-axis space and avoid overlapping with the data.

Future improvements:

- On the hover tooltip, I would change the header from "xx.xx" to "Time xx.xx".
- I would add a menu to select which subplots to show/hide.
- I would like to add a general setting menu to allow users to choose between 1 plot with multiple lines or multiple subplots.
- I would add a unit conversion button for µV and mV
- Fix sliding issues when zoomed in/out, it causes the slider to be offset.
