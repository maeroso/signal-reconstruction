import React, { useState } from "react";

interface GridColumn {
  field: string;
  headerName: string;
  width?: number;
}

const columns: Array<GridColumn> = [
  { field: "id", headerName: "ID", width: 90 },
  {
    field: "userName",
    headerName: "Nome do usuário",
    width: 150,
  },
  {
    field: "algorithm",
    headerName: "Algoritmo",
    width: 150,
  },
  {
    field: "status",
    headerName: "Status",
    width: 150,
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

const rows = [
  {
    id: 1,
    userName: "Fernando Fernandes",
    algorithm: "CGNE",
    status: "Processado",
    startTime: "12/06/2022 04:44",
    endTime: "12/06/2022 04:46",
    imageSize: "30x30",
    increase: 3,
    iteration: 15,
    image:
      "https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.ctfassets.net%2Fhrltx12pl8hq%2F7yQR5uJhwEkRfjwMFJ7bUK%2Fdc52a0913e8ff8b5c276177890eb0129%2Foffset_comp_772626-opt.jpg%3Ffit%3Dfill%26w%3D800%26h%3D300&imgrefurl=https%3A%2F%2Fwww.shutterstock.com%2Fpt%2Ffile-converter&tbnid=MOAYgJU89sFKnM&vet=12ahUKEwjaq96hvKf4AhUTupUCHZN-BtUQMygCegUIARDZAQ..i&docid=f4vxGaCvDKAjnM&w=800&h=300&q=image&ved=2ahUKEwjaq96hvKf4AhUTupUCHZN-BtUQMygCegUIARDZAQ",
  },
  {
    id: 2,
    userName: "Fernando Fernandes",
    algorithm: "CGNE",
    status: "Processado",
    startTime: "12/06/2022 04:46",
    endTime: "12/06/2022 04:50",
    imageSize: "60x60",
    increase: 2,
    iteration: 27,
    image:
      "https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.ctfassets.net%2Fhrltx12pl8hq%2F7yQR5uJhwEkRfjwMFJ7bUK%2Fdc52a0913e8ff8b5c276177890eb0129%2Foffset_comp_772626-opt.jpg%3Ffit%3Dfill%26w%3D800%26h%3D300&imgrefurl=https%3A%2F%2Fwww.shutterstock.com%2Fpt%2Ffile-converter&tbnid=MOAYgJU89sFKnM&vet=12ahUKEwjaq96hvKf4AhUTupUCHZN-BtUQMygCegUIARDZAQ..i&docid=f4vxGaCvDKAjnM&w=800&h=300&q=image&ved=2ahUKEwjaq96hvKf4AhUTupUCHZN-BtUQMygCegUIARDZAQ",
  },
];

interface DataGridProps {
  columns: Array<GridColumn>;
  rows: Array<any>;
}

/* const Header: React.FC<Array<GridColumn>> = (props: Array<GridColumn>) => {
  const columns: Array<GridColumn> = props
  const headers = []
  for(let column of columns) {
    headers.push(<th>{ column.headerName }</th>)
  }
  return headers
} */

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
  for (let row of rows) {
    data.push(
      <tr>
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
          key={row.startTime + "-" + row.id}
        >
          {row.startTime}
        </td>
        <td
          style={{
            border: "1px solid #f1f1f1",
            padding: "10px",
            textAlign: "center",
          }}
          key={row.endTime + "-" + row.id}
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
          key={row.iteration + "-" + row.id}
        >
          <button
            style={{
              backgroundColor: "#95cf",
              color: "#fff",
              border: "none",
              borderRadius: "5px",
              padding: "5px",
            }}
            onClick={ ()=> { handleOpenImage(row.image) } }
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

const JobsTable: React.FC = () => {
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
      <DataGrid columns={columns} rows={rows} />
    </div>
  );
};

export default JobsTable;
