export function days_since(date) {
    const targetDate = new Date(date);
    const today = new Date();

    targetDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    const diffInMs = today - targetDate;
    const diffInDays = Math.round(diffInMs / (1000 * 60 * 60 * 24))

    if (diffInDays === 0){
        return 'Today'
    } else if (diffInDays === 1) {
        return 'Yesterday'
    } else {
        return diffInDays + ' days ago'
    }
}
