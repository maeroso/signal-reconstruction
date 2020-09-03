import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Papa from "papaparse";
import axios from "axios";

class FileReader extends React.Component {
  constructor() {
    super();
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
    const { csvFile } = this.state;
    Papa.parse(csvFile, {
      complete: this.updateData,
      header: false,
    });
  };

  signalIncrement = (inputVector) => {
    const { numberOfSamples, numberOfTransducer } = this.state;

    const returnVector = inputVector;

    for (let lineIndex = 0; lineIndex < numberOfSamples; lineIndex++) {
      /**
       * I preferred to use two "for" instead of a "map",
       * because I wanted to avoid repeating the square root calculation
       * at each position of the vector
       */
      const sumValue = (1 / 20) * lineIndex * Math.sqrt(lineIndex);

      for (let columIndex = 0; columIndex < numberOfTransducer; columIndex++) {
        const flatMatrixIndex = lineIndex + columIndex * numberOfSamples;

        returnVector[flatMatrixIndex] = inputVector[flatMatrixIndex] + sumValue;
      }
    }

    return returnVector;
  };

  updateData(result) {
    this.setState({ data: result.data });
    console.log(this.state.data);

    const g_incrementado = this.signalIncrement(this.state.data);

    const body = {
      g: g_incrementado,
    };

    console.log(g_incrementado);

    axios.post("http://localhost:3333/upload", body).then(function (response) {
      console.log("salvo com sucesso", response);
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
        <p />
        <button onClick={this.importCSV}> Upload now!</button>
      </div>
    );
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <FileReader />
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
