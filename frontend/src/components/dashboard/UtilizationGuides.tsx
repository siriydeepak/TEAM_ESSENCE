import { getUtilizationGuides } from '../../data/mockData'

interface UtilizationGuidesProps {
  productName: string
  isExpired: boolean
}

export default function UtilizationGuides({ productName, isExpired }: UtilizationGuidesProps) {
  if (!isExpired) return null
  
  const guides = getUtilizationGuides(productName)
  
  if (guides.length === 0) return null

  return (
    <div className="mt-4 pt-4 border-t-2 border-[#eeeeed]">
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined neon-text-yellow text-xl">recycling</span>
        <h4 className="font-['Space_Grotesk'] text-sm font-bold text-[#1a1c1c] uppercase tracking-wider">
          Don't Waste It! Utilize It
        </h4>
      </div>
      
      <div className="space-y-2">
        {guides.slice(0, 3).map((guide) => (
          <a
            key={guide.id}
            href={guide.guide_url}
            target="_blank"
            rel="noopener noreferrer"
            className="block p-3 bg-[rgba(255,215,0,0.05)] rounded-xl border border-[rgba(255,215,0,0.2)] hover:border-[#FFD700] hover:shadow-[0_0_15px_rgba(255,215,0,0.3)] transition-all group"
          >
            <div className="flex items-start gap-3">
              <div className="w-16 h-16 rounded-lg overflow-hidden shrink-0">
                <img 
                  src={guide.image} 
                  alt={guide.title}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="flex-1 min-w-0">
                <h5 className="font-['Plus_Jakarta_Sans'] text-sm font-semibold text-[#1a1c1c] mb-1 group-hover:neon-text-yellow transition-colors">
                  {guide.title}
                </h5>
                <p className="text-xs text-[#71717a] font-['Plus_Jakarta_Sans'] mb-2 line-clamp-2">
                  {guide.description}
                </p>
                <div className="flex items-center gap-2 text-xs">
                  <span className={`px-2 py-0.5 rounded-full font-bold uppercase ${
                    guide.difficulty === 'easy' ? 'bg-[rgba(0,255,209,0.1)] text-[#006b57]' :
                    guide.difficulty === 'medium' ? 'bg-[rgba(255,215,0,0.1)] text-[#ff8a00]' :
                    'bg-[rgba(255,51,102,0.1)] text-[#ba1a1a]'
                  }`}>
                    {guide.difficulty}
                  </span>
                  <span className="text-[#71717a]">⏱ {guide.time_required}</span>
                  <span className="ml-auto text-[#006b57] font-semibold flex items-center gap-1">
                    View Guide
                    <span className="material-symbols-outlined text-sm">arrow_forward</span>
                  </span>
                </div>
              </div>
            </div>
          </a>
        ))}
      </div>
      
      <p className="text-xs text-[#71717a] text-center mt-3 font-['Plus_Jakarta_Sans']">
        💡 Click any guide to learn how to repurpose expired items
      </p>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </div>
  )
}
