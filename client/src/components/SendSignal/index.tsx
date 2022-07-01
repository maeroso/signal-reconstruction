import React, { useState } from "react";
import axios, { AxiosResponse } from "axios";
import Papa from "papaparse";
import { Container, SendButton, Row } from "./styles";
import { FiUploadCloud } from "react-icons/fi";
import Select from "react-select";
import FileLoad from "../../components/FileLoadButton";
import { useUser } from "../../userContext";

const SendSignal: React.FC = () => {
  const [file, setFile] = useState<File | undefined>(undefined);
  const [imageSize, setImageSize] = useState<number>(30);
  const [algorithm, setAlgorithm] = useState<number>(1);
  const [increaseRep, setIncreaseRep] = useState<number>(0);
  const { email } = useUser()

  const sizeOptions = [
    { value: 30, label: "30x30" },
    { value: 60, label: "60x60" },
  ];

  const algorithmOptions = [
    { value: 1, label: "CGNE" },
    { value: 2, label: "CGNR" },
    { value: 3, label: "Fista" },
  ];

  const increaseOptions = [
    // { value: 0, label: "0" },
    { value: 1, label: "1" },
    { value: 2, label: "2" },
    { value: 3, label: "3" },
    { value: 4, label: "4" },
    { value: 5, label: "5" },
    { value: 6, label: "6" },
    { value: 7, label: "7" },
    { value: 8, label: "8" },
    { value: 9, label: "9" },
    { value: 10, label: "10" },
  ];

  function uploadFileHandle(): void {
    if (!file) {
      return;
    }

    Papa.parse<string>(file, {
      complete: (csv: Papa.ParseResult<string>) =>
        uploadCSV(signalIncrement(csv), file),
      header: false,
      delimiter: "\r\n",
      transform(value: string): string {
        return value.replace(",", ".").replace("E", "e");
      },
    });
  }

  function signalIncrement(csv: Papa.ParseResult<string>): number[] {
    const numberOfTransducer = 64;
    const numberOfSamples = imageSize === 60 ? 794 : 436;
    const returnVector: number[] = [];

    for (let i = 0; i < increaseRep; i++) {
      for (let lineIndex = 0; lineIndex < numberOfSamples; lineIndex++) {
        /**
         * I preferred to use two "for" instead of a "map",
         * because I wanted to avoid repeating the square root calculation
         * at each position of the vector
         */

        const multiplicationValue =
          100 + (1 / 20) * (lineIndex + 1) * Math.sqrt(lineIndex + 1);

        for (
          let columnIndex = 0;
          columnIndex < numberOfTransducer;
          columnIndex++
        ) {
          const flatMatrixIndex = lineIndex + columnIndex * numberOfSamples;

          returnVector[flatMatrixIndex] =
            parseFloat(csv.data[flatMatrixIndex]) * multiplicationValue;
        }
      }
    }

    return increaseRep > 0 ? returnVector : csv.data.map(Number);
  }

  function uploadCSV(csv: number[], file: File): void {
    const requestJson = { g: csv, alg: algorithm, imageSize, increaseRep, email, fileName: file.name };

    axios
      .post("http://localhost:3333/upload", requestJson)
      .then(function (response: AxiosResponse<any>) {
        console.log("save successfully", response);
      });
  }

  const handleImageSize = (event: any) => {
    setImageSize(event.value);
  };
  const handleAlgorithm = (event: any) => {
    setAlgorithm(event.value);
  };
  const handleIncreaseRep = (event: any) => {
    setIncreaseRep(event.value);
  };

  return (
    <Container>
      <FiUploadCloud size={60} />
      <Row style={{ margin: "20px 0 -20px 0" }}>
        <Select
          options={sizeOptions}
          defaultValue={sizeOptions[0]}
          onChange={handleImageSize}
        />
        <Select
          options={algorithmOptions}
          defaultValue={algorithmOptions[0]}
          onChange={handleAlgorithm}
        />
        <Select
          options={increaseOptions}
          defaultValue={increaseOptions[0]}
          onChange={handleIncreaseRep}
        />
      </Row>
      <Row>
        <FileLoad
          callBackFunction={(selectedFile: File | undefined) =>
            setFile(selectedFile)
          }
        />
        <SendButton onClick={uploadFileHandle} style={{ marginLeft: '18px' }}>Enviar arquivo</SendButton>
      </Row>
    </Container>
  );
};

export default SendSignal;
