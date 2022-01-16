import React, { useEffect, useState } from 'react';
import axios from "axios";
import { AboutCard } from '../about/AboutCard';
import { GetOrders } from '../../api/GetOrders';
import { OrdersTable } from './OrdersTable';
import { IOrder } from "../../customTypes";

export const Orders: React.FC = () => {
  return (
    <>
      <OrdersTable></OrdersTable>
    </>
  );
};