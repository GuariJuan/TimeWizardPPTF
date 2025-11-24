export interface IPrediction {
    t_design:   number;
    t_frontend: number;
    t_backend:  number;
    t_qa:       number;
}

export interface IPredictions {
    predictions: IPrediction;
}
