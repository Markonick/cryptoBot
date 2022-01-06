import React, { useState, useEffect } from 'react';
import { ITick } from '../../customTypes';


type Props = {
    symbol: string,
    currency: string,
};

export const Ticker: React.FC<Props> = (props: Props) => {
    const [tick, setTick] = useState<ITick>({} as ITick);
    const [price, setPrice] = useState<number>(0);
    const [change, setChange] = useState<number>(0);
    // console.log(props.symbol)
    const { symbol, currency } = props;
    const symbolTicker = () => {
        console.log("!!!!!!!!!!!!!!!!!!!!  inside symbolticker  !!!!!!!!!!!!!!!!!!")
        console.log("!!!!!!!!!!!!!!!!!!!!  inside symbolticker  !!!!!!!!!!!!!!!!!!")
        const symbolCurrency = `${symbol.toLowerCase()}${currency}`;
        const ws = new WebSocket(`ws://127.0.0.1:8000/ws/tickers/${symbolCurrency}`);
        console.log(`ws://127.0.0.1:8000/ws/tickers/${symbolCurrency}`)
        ws.onopen = () => {
            console.log('/OPEN')
            ws.send(symbolCurrency);
        };
        ws.onmessage = (event) => {
            // console.log(event)
            let incomingTick = JSON.parse(event.data);
            setTick(incomingTick)
        };
        ws.onclose = () => {
            ws.close();
        };

        return () => {
            ws.close();
        };
    }
    
    // Effect to initialise ticker on render (eg first render or refresh)
    useEffect(() => {
        console.log("!!!!!!!!!!!!!!!!!!!!  inside useEFFECT  !!!!!!!!!!!!!!!!!!")
        console.log("!!!!!!!!!!!!!!!!!!!!  inside useEFFECT  !!!!!!!!!!!!!!!!!!")
        console.log("!!!!!!!!!!!!!!!!!!!!  inside useEFFECT  !!!!!!!!!!!!!!!!!!")
        console.log("!!!!!!!!!!!!!!!!!!!!  inside useEFFECT  !!!!!!!!!!!!!!!!!!")
        symbolTicker();
    }, [props.symbol])
    
    useEffect(() => {   
        let oldPrice = price;
        let newPrice = Number(tick.last_price)
        let calculatedChange:number = calcChange(oldPrice, newPrice)
        setChange(1)
        setPrice(newPrice)
    }, [tick.last_price])

    const calcChange = (prevPrice: number, newPrice: number) => {
        let change = newPrice - prevPrice

        return change
    }

    // return <div>{{ price: price }}</div>
    // symbolTicker(props.symbol, props.currency)
    console.log(tick)
    console.log(typeof tick)
    // return { price: price }
    return <div>{price}{ change}</div>
    // return <li key="crypto">{price}{change}</li>
};

export default Ticker;