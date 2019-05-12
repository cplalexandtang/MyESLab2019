import React, { Component } from 'react'

export default class WSItem extends Component {
  render() {
    return (
      <div className='wsapp-item'>
        <h2>{this.props.name}</h2>
        <img className='item-image' src={this.props.img_url} alt='' />
        <p>{this.props.data + ' ' + this.props.unit}</p>
      </div>
    )
  }
}
