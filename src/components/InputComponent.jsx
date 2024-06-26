import React, { useState } from 'react';
import gtsIcon from '../assets/gtsIcon.png';

function InputComponent() {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // console.log('Form submitted with input:', inputValue);
    setInputValue('');
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 text-center mb-4">
          <img src={gtsIcon} alt="GTS Icon" style={{ maxWidth: '100%' }} />
        </div>
      </div>

      <div className="row justify-content-center mt-3">
        <div className="col-md-6">
          <form onSubmit={handleSubmit}>
            <div className='form-div'>
              <div className="form-group">
                <input
                  type="text"
                  className="form-control"
                  id="inputField"
                  value={inputValue}
                  onChange={handleInputChange}
                  required
                  placeholder='Enter The URL'
                />
              </div>
              <div className="d-grid gap-2">
                <button type="submit" className="btn btn-primary">Verify</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default InputComponent;


