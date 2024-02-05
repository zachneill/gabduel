import logo from './logo.svg';
import './App.css';
import '@mantine/core/styles.css';
import { MantineProvider} from '@mantine/core'
import { ColorSchemeScript } from '@mantine/core';

function App() {
  return (
      <MantineProvider>
       <ColorSchemeScript />

    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="btn btn-primary"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
      </MantineProvider>
  );
}

export default App;
