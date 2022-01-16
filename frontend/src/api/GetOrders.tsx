import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";
import { IOrder, IOrderResponse } from "../customTypes";

export const GetOrders = (page: number, rowsPerPage: number) => {
  const [orders, setOrders] = useState<IOrder[]>([]);
  const [count, setCount] = useState<number>(10);
  // const baseUrl = process.env.REACT_APP_BASE_URL;
  const baseUrl = 'http://localhost:8000';
  const params = { pageNumber: page, pageSize: rowsPerPage }
  useEffect(() => {
    const fetchOrders = async () => {
      console.log('BEFORE FETCHING ORDERS')
      await axios.get<IOrderResponse>(`${baseUrl}/orders`, {params}).then(response => {
        console.log(response?.data)
        setOrders(response?.data.orders);
        setCount(response?.data.count);
      });
    };
    fetchOrders();
  }, []);

  return (
    { "orders": orders, "count": count } 
  );
}
