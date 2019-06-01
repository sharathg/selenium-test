# selenium-test
Test Website using Selenium (https://www.thuisbezorgd.nl)

## Requirements
* Python 3.7 (3.4+)
* Firefox + Geckodriver (Both added to PATH)
* Chrome + Chromedriver (Both added to PATH)


## Setup
* Install dependencies from requirements.txt:  
    <code>pip install -r requirements.txt</code>
* Environment Variables: Set <code>BROWSER</code> as the required browser name.  
    Default is <code>chrome</code>


## Run Tests
* Run on both Firefox and Chrome (One after another)  
    <code>sh run_tests.sh</code>

* All Tests with junit xml  
    <code>python runner.py</code>

* All Tests using unittest test detection  
    <code>python -m unittest</code>

* Specific TestFile/TestClass/TestMethod  
    <code>python -m unittest TestFile.TestClass.TestMethod</code>


## Logs and Reports
* Test Reports will be generated in <code>test-reports</code> folder.  
* Test Script Log will be generated as <code>script.log</code>