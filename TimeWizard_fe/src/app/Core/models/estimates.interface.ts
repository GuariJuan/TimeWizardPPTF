export interface IEstimates {
    batch_predictions: BatchPrediction[];
}

export interface BatchPrediction {
    input:       Input;
    predictions: Predictions;
}

export interface Input {
    s_frontend:       number;
    s_backend:        number;
    lf_react:         number;
    lf_angular:       number;
    lf_javascript:    number;
    lb_node:          number;
    lb_dotnet:        number;
    lb_java:          number;
    Complexity_value: number;
}

export interface Predictions {
    t_design:   number;
    t_frontend: number;
    t_backend:  number;
    t_qa:       number;
}
