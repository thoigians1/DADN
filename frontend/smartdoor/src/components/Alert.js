import React from 'react'

const Alert = ({closeModal}) => {
    const OVERLAY_STYLES = {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, .7)',
        zIndex: 1000
      }
    const MODAL_STYLES = {
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        backgroundColor: '#FFF',
        borderRadius: '25px',
        padding: '50px',
        zIndex: 1000,
      }
  return (
    <div style={OVERLAY_STYLES}>
        <div style={MODAL_STYLES}>
            <h1>Quá số lượng người vào phòng.</h1>
            <div style={{display:'flex', justifyContent:'center'}}>
                <button className='btn' onClick={()=>closeModal()}>Confirm</button>
            </div>
        </div>
    </div>
  )
}

export default Alert