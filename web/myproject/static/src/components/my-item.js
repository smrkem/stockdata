import React from 'react';

export default class MyItem extends React.Component {
    handleThisButton(event) {
        event.preventDefault();
        // do some stuff.
    }

    render() {
        return (
            <tr>
                <td>this item's data in: props.items.key_1</td>
                <td>this item's data in: props.items.key_2</td>
                <td><button onClick={this.handleThisButton}>Click Me</button></td>
            </tr>
        );
    }
}
