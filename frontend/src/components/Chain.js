import React from 'react'

const Chain = ({ onUpdate, chkbox, name, id }) => (
      <div className="chain">
      <input
        type="checkbox"
        key={id}
        checked={chkbox}
        onChange={onUpdate} // dispatch!
        name={name}/>
        <label
            htmlFor={name}
        >
          {name}
        </label>
      </div>
    )


export default Chain