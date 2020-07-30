import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Papa from "papaparse";

class FileReader extends React.Component {
  constructor() {
    super();
    this.state = {
      csvfile: undefined,
      data: undefined,
    };
    this.updateData = this.updateData.bind(this);
  }

  handleChange = (event) => {
    this.setState({
      csvfile: event.target.files[0],
    });
  };

  importCSV = () => {
    const { csvfile } = this.state;
    Papa.parse(csvfile, {
      complete: this.updateData,
      header: false,
    });
  };

  incrementaSinalXVezes = (vetor, numeroDeIncrementos) => {
    let vetorDeRetorno = vetor;
    for (let contador = 0; contador < numeroDeIncrementos; contador++) {
      vetorDeRetorno = vetorDeRetorno.map((value, index) => {
        return value * 100 + (1 / 20) * index * Math.sqrt(index);
      });
    }
    return vetorDeRetorno;
  };

  updateData(result) {
    this.setState({ data: result.data });
    console.log(this.state.data);
    console.log(this.incrementaSinalXVezes(this.state.data, 80));
  }

  render() {
    console.log(this.state.csvfile);

    return (
      <div className="App">
        <h2>Import CSV File!</h2>
        <h4>O resultado irá aparecer no console</h4>
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
