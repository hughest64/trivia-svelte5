export interface SocketMessage {
    type: string;
    message?: string|number|Record<string, unknown>;
}

export type MessageHandler = Record<string, (data?: unknown) => unknown>