import React from 'react'

interface Props {
  callBackFunction: (file: File | undefined) => void
}

const FileLoad: React.FC<Props> = (props: Props) => {
  return (
    <input
      type="file"
      onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
        props.callBackFunction(
          event?.target?.files ? event.target.files[0] : undefined,
        )
      }
    />
  )
}

export default FileLoad
