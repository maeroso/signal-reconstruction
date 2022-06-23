import React, { useState, useEffect } from "react";
import axios, { AxiosResponse } from "axios";
import { useUser } from '../../userContext'

interface GridColumn {
  field: string;
  headerName: string;
}

const columns: Array<GridColumn> = [
  { field: "id", headerName: "ID" },
  {
    field: "userName",
    headerName: "Nome do usuário",
  },
  {
    field: "algorithm",
    headerName: "Algoritmo",
  },
  {
    field: "status",
    headerName: "Status",
  },
  {
    field: "startTime",
    headerName: "Início reconstrução",
  },
  {
    field: "endTime",
    headerName: "Término reconstrução",
  },
  {
    field: "imageSize",
    headerName: "Tamanho pixels",
  },
  {
    field: "increase",
    headerName: "Nr. incrementos",
  },
  {
    field: "iteration",
    headerName: "Nr. iterações",
  },
  {
    field: "image",
    headerName: "Imagem",
  },
];

interface DataGridProps {
  columns: Array<GridColumn>;
  rows: Array<any>;
}

const handleOpenImage = (image: string) => {
  window.open(image)
}

const DataGrid: React.FC<DataGridProps> = (props: DataGridProps) => {
  const columns: Array<GridColumn> = props.columns;
  const headers = [];
  for (let column of columns) {
    headers.push(
      <th
        key={column.field}
        style={{
          border: "1px solid #e1e1e1",
          borderRadius: "5px",
          width: "1px",
          whiteSpace: "nowrap",
          padding: "10px",
          color: "#95cf",
        }}
      >
        {column.headerName}
      </th>
    );
  }

  let data = [];
  for (let row of props.rows) {
    data.push(
      <tr key={'tr-' + row.id}>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.id}
        >
          {row.id}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.userName + "-" + row.id}
        >
          {row.userName}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.algorithm + "-" + row.id}
        >
          {row.algorithm}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.status + "-" + row.id}
        >
          {row.status}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.startTime + "st-" + row.id}
        >
          {row.startTime}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.endTime + "et-" + row.id}
        >
          {row.endTime}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.imageSize + "-" + row.id}
        >
          {row.imageSize}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.increase + "-" + row.id}
        >
          {row.increase}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.iteration + "-" + row.id}
        >
          {row.iteration}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={"btn-" + row.id}
        >
          <button
            style={{
              backgroundColor: "#95cf",
              color: "#fff",
              border: "none",
              borderRadius: "5px",
              padding: "5px",
            }}
            onClick={() => { handleOpenImage(row.image) }}
          >
            Visualizar
          </button>
        </td>
      </tr>
    );
  }
  return (
    <table
      style={{
        color: "#333",
        borderCollapse: "collapse",
        width: "100%",
      }}
    >
      <thead>
        <tr>{headers}</tr>
      </thead>
      <tbody>{data}</tbody>
    </table>
  );
};

const status: any = {
  1: 'Na fila',
  2: 'Processando',
  3: 'Processado'
}

const algorithm: any = {
  1: 'CGNE',
  2: 'CGNR',
  3: 'Fista'
}

const imageSize: any = {
  30: '30x30',
  60: '60x60',
}

interface GridRow {
  id: number,
  userName: string,
  algorithm: string,
  status: string,
  startTime: string,
  endTime: string,
  imageSize: string,
  increase: number,
  iteration: number,
  image: string,
}

const fetchJobs = async (email: string, userName: string) => {
  const jobs: Array<GridRow> = []
  const response = await axios.get("http://localhost:3333/jobs/" + email)
  if (response.data.jobs) {
    response.data.jobs.forEach((item: any) => {
      jobs.push({
        id: item.id,
        userName: userName,
        algorithm: algorithm[item.algorithm],
        status: status[item.status],
        startTime: new Date(1655024068544).toLocaleString(),
        endTime: new Date(1655024068544).toLocaleString(),
        imageSize: imageSize[item.pixelSize],
        increase: item.signalIncreaseRep,
        iteration: item.iterations,
        image: 'http://localhost:3333/images/' + item.id + '.bmp',
      })
    })
    return jobs
  }
}

const firstJobsFetch = async (email: string, userName: string, setJobs: any) => {
  const newJobs: any = await fetchJobs(email, userName);
  setJobs(newJobs)
} 

const JobsTable: React.FC = () => {
  const { email, userName } = useUser();
  const { jobs, setJobs } = useUser()

  //firstJobsFetch(email, userName, setJobs)
  setInterval(async () => {
    const newJobs: any = await fetchJobs(email, userName);
    setJobs(newJobs)
  }, 20000);

  return (
    <div
      style={{
        height: 400,
        width: "87vw",
        boxShadow: "1px 1px 3px rgba(55, 55, 55, 0.5)",
        borderRadius: "5px",
        marginLeft: "10px",
        backgroundColor: "#fff",
      }}
    >
      <DataGrid columns={columns} rows={jobs} />
    </div>
  );
};

export default JobsTable;
