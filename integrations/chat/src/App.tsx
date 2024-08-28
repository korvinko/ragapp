import { ChatBotWidget } from './components/Chat';

const App = () => {

    return <div>
        <ChatBotWidget apiURL='http://localhost:8000/ask' />
    </div>;
};

export default App;
