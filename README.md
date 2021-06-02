# Octopus Energy Usage
Python script to call Octopus Energy's API to gather your energy usage between a specified date range.

To use the script, you will need to have Python installed along with the following libraries:
- Pandas
- Requests

You will also need to provide the script with your customer API key, MPAN, MPRN and meter serial numbers.
Your API key can be found by logging into you Octopus account, whereas the MPAN, MPRN and meter serial numbers can be found within the settings of your smart meter device.
Once you have the API key and relevant numbers, enter these into the script where idicated within the quotes.

Once the script has successfully run, it will produce a CSV file with your usage data within the same directory as your script's saved location.
