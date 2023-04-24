import React, { useState, useEffect, useRef } from 'react';
import _ from "lodash";

function useInterval(callback: any, delay: any) {
    const savedCallback = useRef();

    useEffect(() => {
        savedCallback.current = callback;
    }, [callback]);

    useEffect(() => {
        function tick() {
            // @ts-ignore
            savedCallback.current()
        }
        if (delay !== null) {
            let id = setInterval(tick, delay);
            return () => clearInterval(id);
        }
    }, [delay]);
}

export {
    useInterval
};