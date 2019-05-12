import React from 'react'
import WSItem from './WSItem'


class WSApp extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      temperature: 0,
      pressure: 0,
      humidity: 0,
      windDirection: 0
    }
  }

  componentDidMount() {
    setInterval(() => this.update(), 1000);
  }

  update = () => {
    fetch('WeatherStation/')
      .then(res => res.json())
      .then(value => { this.setState(() => value) });
  }

  render() {
    return (
      <div className='wsapp'>
        <h1>Weather Station App</h1>
        <WSItem name='Temperature' unit='°C' img_url={require('./pictures/termometer.png')} data={this.state.temperature} />
        <WSItem name='Pressure' unit='Pa' img_url={require('./pictures/pressure.png')} data={this.state.pressure} />
        <WSItem name='Humidity' unit='%' img_url={require('./pictures/humidity.png')} data={this.state.humidity} />
        <WSItem name='Wind Direction' unit='°' img_url={require('./pictures/magnemometer.png')} data={this.state.windDirection} />
      </div>
    )
  }
}

export default WSApp;