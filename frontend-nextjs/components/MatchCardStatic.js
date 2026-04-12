import { ExternalLink, MapPin, Shield } from 'lucide-react'

export default function MatchCardStatic({ match }) {
  const scoreColor = match.matchScore >= 90
    ? 'bg-emerald-50 text-emerald-600 border-emerald-100'
    : match.matchScore >= 80
    ? 'bg-amber-50 text-amber-600 border-amber-100'
    : 'bg-gray-50 text-slate-500 border-gray-100'

  return (
    <div className="break-inside-avoid mb-4 bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-lg hover:border-gray-200 transition-all duration-300">
      {/* Gradient placeholder */}
      <div className="relative h-32 bg-gradient-to-br from-slate-100 to-slate-200">
        {/* Source badge */}
        <div className="absolute top-2.5 right-2.5 flex items-center gap-1.5 bg-white/90 backdrop-blur-sm rounded-full px-2.5 py-1">
          <span className="w-2 h-2 rounded-full" style={{ backgroundColor: match.source.color }} />
          <span className="text-[10px] font-semibold text-slate-700">{match.source.name}</span>
        </div>
        {/* Score badge */}
        <div className={`absolute bottom-2.5 left-2.5 flex items-center gap-1 rounded-full border px-2 py-0.5 ${scoreColor}`}>
          <span className="text-[10px] font-bold">{match.matchScore}%</span>
          <span className="text-[9px]">match</span>
        </div>
        {/* Featured */}
        {match.featured && (
          <div className="absolute bottom-2.5 right-2.5 bg-amber-400 text-white text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full">
            Featured
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="text-sm font-semibold text-slate-900 line-clamp-2 leading-snug">{match.title}</h3>
        <p className="mt-1.5 text-base font-bold text-slate-900">{match.formattedPrice}</p>

        <div className="mt-2 flex items-center gap-3 text-[11px] text-slate-400">
          <span className="flex items-center gap-1">
            <MapPin className="w-3 h-3" />
            {match.location}
          </span>
          <span>{match.postedAgo}</span>
        </div>

        {/* Specs */}
        {match.specs?.length > 0 && (
          <div className="mt-2.5 flex flex-wrap gap-1">
            {match.specs.map((spec) => (
              <span key={spec} className="rounded-full bg-gray-100 px-2 py-0.5 text-[11px] font-medium text-slate-500">
                {spec}
              </span>
            ))}
          </div>
        )}

        {/* Seller tag */}
        {match.sellerTag && (
          <div className="mt-2.5 flex items-center gap-1 text-[11px] font-medium text-emerald-600">
            <Shield className="w-3 h-3" />
            {match.sellerTag}
          </div>
        )}

        {/* Open link */}
        <a
          href={match.source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-3 flex items-center justify-center gap-1.5 w-full rounded-xl bg-gray-50 hover:bg-sky-50 border border-gray-100 hover:border-sky-200 py-2.5 text-xs font-semibold text-slate-600 hover:text-sky-600 transition-all"
        >
          Open on {match.source.name}
          <ExternalLink className="w-3 h-3" />
        </a>
      </div>
    </div>
  )
}
