import _ from 'lodash';
import React from 'react';
import ItemsBoardHeader from './items-board-header'
import MyItem from './my-item'

export default class ItemsBoard extends React.Component {
    renderItems() {
        return _.map(this.props.items, (myItem, index) => <MyItem key={index} {...myItem} />);
    }

    render() {
        return (
            <table>
                <ItemsBoardHeader />
                <tbody>
                    {this.renderItems()}
                </tbody>
            </table>
        );
    }
}
