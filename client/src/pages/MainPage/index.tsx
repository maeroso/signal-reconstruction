import axios, { AxiosResponse } from 'axios'
import Papa from 'papaparse'
import React, { useState } from 'react'
import FileLoad from '../../components/FileLoadButton'

const MainPage: React.FC<void> = () => {
  const numberOfTransducer = 64
  const numberOfSamples = 794
  const [file, setFile] = useState<File | undefined>(undefined)

  function uploadFileHandle(): void {
    if (!file) {
      return
    }

    Papa.parse<string>(file, {
      complete: (csv: Papa.ParseResult<string>) =>
        uploadCSV(signalIncrement(csv)),
      header: false,
      delimiter: '\r\n',
      transform(value: string): string {
        return value.replace(',', '.').replace('E', 'e')
      },
    })
  }

  function signalIncrement(csv: Papa.ParseResult<string>): number[] {
    const returnVector: number[] = []

    for (let lineIndex = 0; lineIndex < numberOfSamples; lineIndex++) {
      /**
       * I preferred to use two "for" instead of a "map",
       * because I wanted to avoid repeating the square root calculation
       * at each position of the vector
       */

      const multiplicationValue =
        100 + (1 / 20) * (lineIndex + 1) * Math.sqrt(lineIndex + 1)

      for (
        let columnIndex = 0;
        columnIndex < numberOfTransducer;
        columnIndex++
      ) {
        const flatMatrixIndex = lineIndex + columnIndex * numberOfSamples

        returnVector[flatMatrixIndex] =
          parseFloat(csv.data[flatMatrixIndex]) * multiplicationValue
      }
    }

    return returnVector
  }

  function uploadCSV(csv: number[]): void {
    const requestJson = { g: csv, alg: 0 }

    axios
      .post('http://localhost:3333/upload', requestJson)
      .then(function (response: AxiosResponse<any>) {
        console.log('save successfully', response)
      })
  }

  return (
    <div>
      <h1>Página principal</h1>
      <FileLoad
        callBackFunction={(selectedFile: File | undefined) =>
          setFile(selectedFile)
        }
      />
      <button onClick={uploadFileHandle}>Enviar arquivo</button>
    </div>
  )
}

export default MainPage
