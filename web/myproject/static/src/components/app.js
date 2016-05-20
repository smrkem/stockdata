import React from 'react';
import ItemsBoard from './items-board';


// Mock data:
const myitems = [
{
  "some_key_1": 1,
  "some_key_2": {
    "id": 1,
    "foo": "Bar",
  }
},
{
    "some_key_1": 3,
    "some_key_2": {
        "id": 23,
        "foo": "Baz",
    },
    "some_key_3": "Bux"
}
];


var pollingRequest;

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            myitems
        };
    }

    getItems() {
        $.ajax({
            url: '/myapp/items',
            dataType: 'json',
            cache: false,
            success: (data) => {
                this.setState({myitems: data});
            },
            error: (xhr, status, err) => {
                console.log(xhr.statusText);
                alert('error retrieving items data. is the remote API running and accessible?');
                if (pollingRequest) {
                    clearInterval(pollingRequest);
                    pollingRequest = false;
                }
            }
        });
    }

    componentDidMount() {
        pollingRequest = setInterval(this.getItems.bind(this), 2000);
    }

    render() {
        return (
            <div>
                <h1>Items Board</h1>
                <ItemsBoard items={this.state.myitems} />
            </div>
        );
    }
}
