import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Papa from "papaparse";
import axios from "axios";

class FileReader extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            csvFile: undefined,
            data: undefined,
            numberOfTransducer: 64,
            numberOfSamples: 794,
        };
        this.updateData = this.updateData.bind(this);
    }

    handleChange = (event) => {
        this.setState({
            csvFile: event.target.files[0],
        });
    };

    importCSV = () => {
        const {csvFile} = this.state;
        Papa.parse(csvFile, {
            complete: this.updateData,
            header: false,
            delimiter: '\r\n',
            transform(value, field) {
                return value.replace(',', '.').replace('E', 'e');
            }
        });
    };

    signalIncrement = (inputVector) => {
        const {numberOfSamples, numberOfTransducer} = this.state;
        // debugger;
        const returnVector = inputVector;

        for (let lineIndex = 0; lineIndex < numberOfSamples; lineIndex++) {
            /**
             * I preferred to use two "for" instead of a "map",
             * because I wanted to avoid repeating the square root calculation
             * at each position of the vector
             */
            const multiplicationValue = 100 +(1 / 20) * (lineIndex + 1) * Math.sqrt(lineIndex + 1);

            for (let columnIndex = 0; columnIndex < numberOfTransducer; columnIndex++) {
                const flatMatrixIndex = lineIndex + columnIndex * numberOfSamples;

                returnVector[flatMatrixIndex] = parseFloat(inputVector[flatMatrixIndex]) * multiplicationValue;
                // returnVector[flatMatrixIndex] = parseFloat(inputVector[flatMatrixIndex]);
            }
        }

        return returnVector;
    };

    updateData(result) {
        this.setState({data: result.data});
        // debugger;
        console.log(this.state.data);

        const incrementalSignal = this.signalIncrement(
            this.state.data
        );

        const body = {
            g: incrementalSignal,
            alg: 0
        };

        console.log(incrementalSignal);

        axios.post("http://localhost:3333/upload", body).then(function (response) {
            console.log("save successfully", response);
        });
    }

    render() {
        console.log(this.state.csvFile);

        return (
            <div className="App">
                <h2>Import CSV File!</h2>
                <h4>The result will be displayed on the console</h4>
                <input
                    className="csv-input"
                    type="file"
                    ref={(input) => {
                        this.filesInput = input;
                    }}
                    name="file"
                    placeholder={null}
                    onChange={this.handleChange}
                />
                <p/>
                <button onClick={this.importCSV}> Upload now!</button>
            </div>
        );
    }
}

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo"/>
                <FileReader/>
                <p>
                    Edit <code>src/App.js</code> and save to reload.
                </p>
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn React
                </a>
            </header>
        </div>
    );
}

export default App;
