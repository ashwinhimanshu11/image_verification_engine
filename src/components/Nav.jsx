import React from 'react'

function Nav() {
  return (
    <div>
      <div className="nav">
        <button className="b-1">URL Verification</button>
        <button className="b-1">Image Verification</button>
        <p>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            width="24"
            height="24"
            color="#000000"
            fill="none"
          >
            <path
              d="M18.001 8V8.00635M12.001 8V8.00635M6.00098 8L6.00098 8.00635M18.001 15.9937V16M12.001 15.9937V16M6.00098 15.9937L6.00098 16"
              stroke="currentColor"
              stroke-width="2.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </p>
        <button id="btn">Sign in</button>
      </div>
    </div>
  )
}

export default Nav
