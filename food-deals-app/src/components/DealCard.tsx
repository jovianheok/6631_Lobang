type DealCardProps = {
    title: string;
    restaurant: string;
    price: string;
    cuisine: string
};

export default function DealCard({
    title,
    restaurant,
    price,
    cuisine,
}: DealCardProps) {
    return (
        <div className="rounded-xl border p-4 shadow-sm">
            <h2 className="text-2xl font-semibold">{title}</h2>
            
            <p className="mt-2 text-gray-600">{restaurant}</p>

            <div className="mt-4 flex items-center justify-between">
                <span className="rounded-full bg-gray-100 px-3 py-1 text-sm">
                    {cuisine}
                </span>
                
                <span className="font-bold">{price}</span>
            </div>
        </div>
    );
}