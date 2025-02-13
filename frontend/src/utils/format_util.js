function formatKVDict(dict) {
    if (!dict) {
        return null
    }

    const formattedText = Object.entries(dict).map(([key, value]) => {
        try {
            return `${key}:${value.toFixed(2)}`;
        } catch {
            return `${key}:${value}`;
        }
    }).join(';');
    return formattedText
}


export default {
    formatKVDict
}