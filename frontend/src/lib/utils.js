export function days_since(user_score) {
    if (!user_score || (user_score.fail === 0 && user_score.success === 0)) {
        return 'Never'
    }
    
    const targetDate = new Date(user_score.last_try);
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