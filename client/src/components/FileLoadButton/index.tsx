import React from "react";

interface Props {
  callBackFunction: (file: File | undefined) => void;
}

const FileLoad: React.FC<Props> = (props: Props) => {
  return (
    <label style={{
      border: '1px solid #ccc',
      display: 'inline-block',
      padding: '8px 12px',
      cursor: 'pointer',
      borderRadius: '5px'
    }}>
      <input
        style={{ display: 'none' }}
        type="file"
        onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
          props.callBackFunction(
            event?.target?.files ? event.target.files[0] : undefined
          )
        }
      />
      Procurar arquivo
    </label>
  );
};

export default FileLoad;
